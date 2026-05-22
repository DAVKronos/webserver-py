export const isFolder = (item) => {
  return item.type === 'folder' || item.is_folder === true
}

export const getItemTitle = (item) => {
  return item.name || item.title || item.file_name || 'Untitled'
}

export const getItemLink = (item) => {
  if (isFolder(item)) {
    return `/documents/folder/${item.id}`
  }

  return `/documents/${item.id}`
}