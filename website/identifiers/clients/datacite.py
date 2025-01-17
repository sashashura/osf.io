# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging

import re
import datetime

from website.identifiers.clients.base import AbstractIdentifierClient
from website import settings
from datacite import DataCiteMDSClient, schema43
from django.core.exceptions import ImproperlyConfigured
from osf.metadata.utils import datacite_format_subjects, datacite_format_contributors, datacite_format_creators

logger = logging.getLogger(__name__)


class DataCiteClient(AbstractIdentifierClient):

    def __init__(self, node):
        try:
            assert settings.DATACITE_URL and (getattr(node.provider, 'doi_prefix', None) or settings.DATACITE_PREFIX)
        except AssertionError:
            raise ImproperlyConfigured('OSF\'Datacite client\'s settings are not configured')

        self._client = DataCiteMDSClient(
            url=settings.DATACITE_URL,
            username=settings.DATACITE_USERNAME,
            password=settings.DATACITE_PASSWORD,
            prefix=getattr(node.provider, 'doi_prefix', None) or settings.DATACITE_PREFIX
        )

    def build_metadata(self, node):
        """Return the formatted datacite metadata XML as a string.
         """
        non_bib_contributors = node.contributors.filter(
            contributor__visible=False,
            contributor__node=node.id
        )

        contributors = datacite_format_contributors(non_bib_contributors)
        contributors.append({
            'nameType': 'Organizational',
            'contributorType': 'HostingInstitution',
            'contributorName': 'Open Science Framework',
            'name': 'Open Science Framework',
            'nameIdentifiers': [
                {
                    'name': 'Open Science Framework',
                    'nameIdentifier': f'https://ror.org/{settings.OSF_ROR_ID}/',
                    'nameIdentifierScheme': 'ROR',
                },
                {
                    'name': 'Open Science Framework',
                    'nameIdentifier': f'https://grid.ac/institutes/{settings.OSF_GRID_ID}/',
                    'nameIdentifierScheme': 'GRID',
                }
            ],
        })

        date_created = node.created.date() if not node.type == 'osf.registration' else node.registered_date.date()
        data = {
            'identifiers': [
                {
                    'identifier': self.build_doi(node),
                    'identifierType': 'DOI',
                }
            ],
            'creators': datacite_format_creators(node.visible_contributors),
            'contributors': contributors,
            'titles': [
                {'title': node.title}
            ],
            'publisher': 'Open Science Framework',
            'publicationYear': str(datetime.datetime.now().year),
            'types': {
                'resourceType': 'Pre-registration' if node.type == 'osf.registration' else 'Project',
                'resourceTypeGeneral': 'Text'
            },
            'schemaVersion': 'http://datacite.org/schema/kernel-4',
            'dates': [
                {
                    'date': str(date_created),
                    'dateType': 'Created'
                },
                {
                    'date': str(node.modified.date()),
                    'dateType': 'Updated'
                },
                {
                    'date': str(datetime.datetime.now().date()),
                    'dateType': 'Issued'
                },
            ]
        }

        article_doi = node.article_doi
        if article_doi:
            data['relatedIdentifiers'] = [
                {
                    'relatedIdentifier': article_doi,
                    'relatedIdentifierType': 'DOI',
                    'relationType': 'IsSupplementTo'
                }
            ]

        if node.description:
            data['descriptions'] = [{
                'descriptionType': 'Abstract',
                'description': node.description
            }]

        if node.node_license:
            data['rightsList'] = [{
                'rights': node.node_license.name,
                'rightsURI': node.node_license.url
            }]

        data['subjects'] = datacite_format_subjects(node)

        # Validate dictionary
        assert schema43.validate(data)

        # Generate DataCite XML from dictionary.
        return schema43.tostring(data)

    def build_doi(self, object):
        return settings.DOI_FORMAT.format(
            prefix=getattr(object.provider, 'doi_prefix', None) or settings.DATACITE_PREFIX,
            guid=object._id
        )

    def get_identifier(self, identifier):
        self._client.doi_get(identifier)

    def create_identifier(self, node, category):
        if category == 'doi':
            if settings.DATACITE_ENABLED:
                metadata = self.build_metadata(node)
                resp = self._client.metadata_post(metadata)
                # Typical response: 'OK (10.70102/FK2osf.io/cq695)' to doi 10.70102/FK2osf.io/cq695
                doi = re.match(r'OK \((?P<doi>[a-zA-Z0-9 .\/]{0,})\)', resp).groupdict()['doi']
                self._client.doi_post(doi, node.absolute_url)
                return {'doi': doi}
            logger.info('TEST ENV: DOI built but not minted')
            return {'doi': self.build_doi(node)}
        else:
            raise NotImplementedError('Creating an identifier with category {} is not supported'.format(category))

    def update_identifier(self, node, category):
        if settings.DATACITE_ENABLED and not node.is_public or node.is_deleted:
            if category == 'doi':
                doi = self.build_doi(node)
                self._client.metadata_delete(doi)
                return {'doi': doi}
            else:
                raise NotImplementedError('Updating metadata not supported for {}'.format(category))
        else:
            return self.create_identifier(node, category)
