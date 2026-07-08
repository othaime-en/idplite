/**
 * Wraps a route element and redirects to /login if there's no authenticated
 * user in AuthContext. Because the JWT lives only in memory (never
 * localStorage), this fires on every fresh page load too — that's expected,
 * not a bug: see hooks/useAuth.tsx for the reasoning.
 */
import type { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}