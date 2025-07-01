/**
 * TypeScript type definitions for flight data structures.
 * 
 * These types ensure type safety between the Python backend
 * and TypeScript frontend components.
 */

export interface FlightData {
  flightNumber: string
  model: string
  registration: string
  groundSpeed: number
  altitude?: string | number
  lastUpdated?: string
  totalAircraft?: number
  error?: string
}

export interface Aircraft {
  flightNumber: string
  model: string
  registration: string
  groundSpeed: number
  altitude?: string | number
  hexCode?: string
  latitude?: number
  longitude?: number
  heading?: number
  verticalRate?: number
  squawk?: string
}

export interface FlightInfoDisplayProps {
  flightNumber: string
  model: string
  registration: string
  groundSpeed: number
  loading?: boolean
  totalAircraft?: number
  lastUpdated?: string
}

export interface APIResponse {
  success: boolean
  data?: FlightData
  error?: string
  timestamp: string
} 