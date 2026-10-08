import React from 'react'
import './App.scss'
import { AuthProvider } from './utils/AuthContext'
import { ReactQueryCacheProvider } from 'react-query'
import queryCache from './utils/query-cache'

import './utils/i18n.js'
import AppRouter from './AppRouter'
import CookiesWarning from './components/Generic/CookiesWarning'

const EnvContext = React.createContext({})

const App = (props) => {
  return (
    <EnvContext.Provider value={props}>
      <AuthProvider>
        <ReactQueryCacheProvider queryCache={queryCache}>
          <AppRouter />
          <CookiesWarning />
        </ReactQueryCacheProvider>
      </AuthProvider>
    </EnvContext.Provider>
  )
}

export { EnvContext }

export default App
