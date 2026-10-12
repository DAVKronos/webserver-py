import { QueryCache } from 'react-query'

// Shared so AuthContext can refetch everything when the logged-in user changes.
const queryCache = new QueryCache({
  defaultConfig: {
    queries: {
      refetchOnWindowFocus: false
    }
  }
})

export default queryCache
