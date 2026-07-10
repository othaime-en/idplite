import { createContext, useContext, useState, type ReactNode } from 'react'
import { api, type User } from '../api/client'

// Re-exported for convenience so other files can `import { User } from
// '../hooks/useAuth'` without also reaching into api/client. The type
// itself now lives in api/client.ts (Phase 1 change) so the API client and
// AuthContext never disagree about the User shape.
export type { User }

interface AuthContextValue {
    user: User | null
    token: string | null
    isAuthenticated: boolean
    login: (token: string, user: User) => void
    logout: () => void
}

// Create the context with undefined as the initial value.
// This is intentional — if a component calls useAuth() outside of AuthProvider,
// they'll get an error rather than silently getting null/undefined values.
const AuthContext = createContext<AuthContextValue | undefined>(undefined)

interface AuthProviderProps {
    children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
    // Both pieces of auth state are stored together.
    // When we have a token, we have a user; when we don't, we have neither.
    const [user, setUser] = useState<User | null>(null)
    const [token, setToken] = useState<string | null>(null)

    function login(newToken: string, newUser: User) {
        api.setToken(newToken)
        setToken(newToken)
        setUser(newUser)
    }

    function logout() {
        api.setToken(null)
        setToken(null)
        setUser(null)
    }

    const value: AuthContextValue = {
        user,
        token,
        isAuthenticated: user !== null,
        login,
        logout,
    }

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
    const ctx = useContext(AuthContext)
    if (ctx === undefined) {
        throw new Error('useAuth() must be called inside an <AuthProvider>. Check that App.tsx wraps everything in <AuthProvider>.')
    }
    return ctx
}