import { createBrowserRouter } from 'react-router-dom'

import Home from './pages/Home'
import Games from './pages/Games'

const router = createBrowserRouter([
    {
        path: '/',
        element: <Home />
    },
    {
        path: '/games',
        element: <Games />
    },
])

export { router }