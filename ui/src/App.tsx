import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './hooks/useAuth'

// Phase 0 placeholder pages — replaced with real implementations in Phase 6
function Dashboard() {
    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center">
            <div className="text-center">
                <h1 className="text-3xl font-bold text-white mb-2">IDP Lite</h1>
                <p className="text-gray-400">Dashboard — implemented in Phase 6</p>
                <p className="text-gray-600 text-sm mt-4">
                    If you can see this, Tailwind CSS and React Router are working.
                </p>
            </div>
        </div>
    )
}

function Login() {
    const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 w-96 text-center">
                <h1 className="text-2xl font-bold text-white mb-2">IDP Lite</h1>
                <p className="text-gray-400 mb-8 text-sm">Self-service environment provisioning</p>
                {/* 
          This anchor tag is intentional — it's a full page navigation, not a React Router link.
          We're leaving the browser to go to the FastAPI GitHub OAuth redirect endpoint.
          The API then redirects to GitHub, which then redirects back to our callback URL.
          A React Router <Link> wouldn't work here because we need a real HTTP GET, not a
          client-side navigation.
        */}
                <a
                    href={`${apiUrl}/auth/github`}
                    className="flex items-center justify-center gap-3 bg-white text-gray-900 
                     font-semibold px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors"
                >
                    {/* GitHub SVG icon */}
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                    </svg>
                    Login with GitHub
                </a>
                <p className="text-gray-600 text-xs mt-4">
                    Phase 0 stub — full OAuth flow implemented in Phase 1
                </p>
            </div>
        </div>
    )
}

function NotFound() {
    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center">
            <div className="text-center">
                <p className="text-gray-600 font-mono text-6xl mb-4">404</p>
                <p className="text-gray-400">Page not found</p>
            </div>
        </div>
    )
}

export default function App() {
    return (
        /*
         * AuthProvider wraps everything so any component can call useAuth() to get
         * the current user without needing to pass it down through props.
         */
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/login" element={<Login />} />
                    {/* <Route path="/new" element={<NewEnvironment />} /> */}
                    {/* <Route path="/environments/:id" element={<EnvironmentDetail />} /> */}
                    {/* <Route path="/audit" element={<AuditLog />} /> */}
                    {/* <Route path="/settings" element={<Settings />} /> */}
                    <Route path="*" element={<NotFound />} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    )
}