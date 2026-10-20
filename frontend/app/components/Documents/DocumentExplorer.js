import React, { useMemo, useState } from 'react'
import { Alert, Breadcrumb, Button, FormControl } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { BsChevronRight, BsFileText, BsFolder, BsSearch } from 'react-icons/bs'
import { useTranslation } from 'react-i18next'
import DefaultSpinner from '../Generic/Spinner'
import { getFolders, getDocuments } from './queries'

const DocumentExplorer = ({ folderId = null }) => {
  const [showAll, setShowAll] = useState(false)
  const [search, setSearch] = useState('')
  const { t } = useTranslation('documentLibrary')

  const safeFolderId =
    folderId && !Number.isNaN(Number(folderId))
      ? Number(folderId)
      : null

  const {
    data: foldersData = [],
    isLoading: foldersLoading,
    isError: foldersError,
    refetch: refetchFolders
  } = useQuery(['folders'], getFolders)

  const {
    data: documents = [],
    isLoading: docsLoading,
    isError: docsError,
    refetch: refetchDocuments
  } = useQuery(
    ['documents', safeFolderId],
    () => getDocuments(safeFolderId),
    { enabled: !!safeFolderId }
  )

  const folders = foldersData.filter((folder) => {
    const parentId = folder.parent_folder_id ?? null
    return safeFolderId
      ? Number(parentId) === safeFolderId
      : parentId === null
  })

  const currentFolder = foldersData.find(folder => Number(folder.id) === safeFolderId)
  const ancestors = useMemo(() => {
    const chain = []
    let parent = currentFolder

    while (parent && chain.length < foldersData.length) {
      chain.unshift(parent)
      parent = foldersData.find(folder => Number(folder.id) === Number(parent.parent_folder_id))
    }

    return chain
  }, [currentFolder, foldersData])

  const normalizedSearch = search.trim().toLocaleLowerCase()
  const filteredFolders = folders.filter(folder =>
    (folder.name || folder.title || '').toLocaleLowerCase().includes(normalizedSearch)
  )
  const filteredDocuments = documents.filter(document =>
    (document.name || document.title || document.file_name || '').toLocaleLowerCase().includes(normalizedSearch)
  )
  const visibleDocuments = showAll ? filteredDocuments : filteredDocuments.slice(0, 8)
  const loading = foldersLoading || (safeFolderId && docsLoading)
  const hasError = foldersError || (safeFolderId && docsError)

  return (
    <section className='document-library'>
      <header className='document-library-header'>
        <div className='document-library-heading'>
          <span className='document-library-eyebrow'>{t('eyebrow')}</span>
          <h1>{currentFolder ? currentFolder.name : t('title')}</h1>
          <p>{currentFolder ? t('folderDescription') : t('description')}</p>
        </div>

        <div className='document-library-actions'>
          <Link to={safeFolderId ? `/folders/new?parent=${safeFolderId}` : '/folders/new'} className='document-library-action'>
            <BsFolder aria-hidden='true' />
            {t('newFolder')}
          </Link>
          {safeFolderId && (
            <Link to={`/documents/new?folder=${safeFolderId}`} className='document-library-action document-library-action-primary'>
              <BsFileText aria-hidden='true' />
              {t('newDocument')}
            </Link>
          )}
        </div>
      </header>

      <div className='document-library-toolbar'>
        <Breadcrumb className='document-library-breadcrumb'>
          <Breadcrumb.Item active={!safeFolderId} linkAs={Link} linkProps={{ to: '/folders' }}>
            {t('root')}
          </Breadcrumb.Item>
          {ancestors.map((folder, index) => (
            <Breadcrumb.Item
              key={folder.id}
              active={index === ancestors.length - 1}
              linkAs={Link}
              linkProps={{ to: `/folders/${folder.id}` }}
            >
              {folder.name}
            </Breadcrumb.Item>
          ))}
        </Breadcrumb>

        <div className='document-library-search'>
          <BsSearch aria-hidden='true' />
          <FormControl
            type='search'
            aria-label={t('search')}
            placeholder={t('search')}
            value={search}
            onChange={event => setSearch(event.target.value)}
          />
        </div>
      </div>

      {hasError && (
        <Alert variant='danger' className='document-library-error'>
          <div>
            <strong>{t('loadErrorTitle')}</strong>
            <div>{t('loadErrorDescription')}</div>
          </div>
          <Button
            variant='outline-danger'
            size='sm'
            onClick={() => {
              refetchFolders()
              if (safeFolderId) refetchDocuments()
            }}
          >
            {t('retry')}
          </Button>
        </Alert>
      )}

      {loading && <div className='document-library-loading'><DefaultSpinner /></div>}

      {!foldersLoading && !foldersError && (
        <section className='document-library-section' aria-labelledby='document-folders-heading'>
          <div className='document-library-section-heading'>
            <div>
              <span className='document-library-section-icon'><BsFolder aria-hidden='true' /></span>
              <h2 id='document-folders-heading'>{t('folders')}</h2>
            </div>
            <span className='document-library-count'>{filteredFolders.length}</span>
          </div>

          {filteredFolders.length > 0
            ? (
              <div className='document-library-grid'>
                {filteredFolders.map(folder => {
                  const childCount = foldersData.filter(item => Number(item.parent_folder_id) === Number(folder.id)).length
                  return (
                    <Link className='document-entry document-entry-folder' to={`/folders/${folder.id}`} key={folder.id}>
                      <span className='document-entry-icon'><BsFolder aria-hidden='true' /></span>
                      <span className='document-entry-copy'>
                        <span className='document-entry-title'>{folder.name || folder.title}</span>
                        <span className='document-entry-meta'>
                          {childCount > 0
                            ? childCount === 1
                              ? t('folderCountOne')
                              : t('folderCount', { count: childCount })
                            : t('openFolder')}
                        </span>
                      </span>
                      <BsChevronRight className='document-entry-chevron' aria-hidden='true' />
                    </Link>
                  )
                })}
              </div>
              )
            : (
              <div className='document-library-empty'>{t(normalizedSearch ? 'noSearchResults' : 'noFolders')}</div>
              )}
        </section>
      )}

      {safeFolderId && (
        <section className='document-library-section document-library-files' aria-labelledby='document-files-heading'>
          <div className='document-library-section-heading'>
            <div>
              <span className='document-library-section-icon document-library-file-icon'><BsFileText aria-hidden='true' /></span>
              <h2 id='document-files-heading'>{t('documents')}</h2>
            </div>
            <span className='document-library-count'>{filteredDocuments.length}</span>
          </div>

          {!docsLoading && !docsError && (
            filteredDocuments.length > 0
              ? (
                <div className='document-library-grid'>
                  {visibleDocuments.map(document => (
                    <Link className='document-entry document-entry-file' to={`/documents/${document.id}`} key={document.id}>
                      <span className='document-entry-icon'><BsFileText aria-hidden='true' /></span>
                      <span className='document-entry-copy'>
                        <span className='document-entry-title'>
                          {document.name || document.title || document.file_name}
                        </span>
                        <span className='document-entry-meta'>{t('openDocument')}</span>
                      </span>
                      <BsChevronRight className='document-entry-chevron' aria-hidden='true' />
                    </Link>
                  ))}
                </div>
                )
              : (
                <div className='document-library-empty'>{t(normalizedSearch ? 'noSearchResults' : 'noDocuments')}</div>
                )
          )}

          {!showAll && filteredDocuments.length > 8 && (
            <div className='document-library-more'>
              <Button variant='outline-success' onClick={() => setShowAll(true)}>
                {t('showAll', { count: filteredDocuments.length })}
              </Button>
            </div>
          )}
        </section>
      )}
    </section>
  )
}

export default DocumentExplorer
