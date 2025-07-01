'use client'

import FlightInfoDisplay from "@/components/flight-info-display"
import { useEffect, useState } from "react"
import { FlightData } from "@/types/flight"

export default function Home() {
  const [flightData, setFlightData] = useState<FlightData>({
    flightNumber: "Loading...",
    model: "Loading...",
    registration: "Loading...",
    groundSpeed: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchFlightData = async () => {
      try {
        const response = await fetch('/api/flight-data')
        const data = await response.json()
        setFlightData(data)
      } catch (error) {
        console.error('Failed to fetch flight data:', error)
        setFlightData({
          flightNumber: "ERROR",
          model: "Unknown",
          registration: "Unknown",
          groundSpeed: 0
        })
      } finally {
        setLoading(false)
      }
    }

    fetchFlightData()
  }, [])

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-100">
      <FlightInfoDisplay 
        flightNumber={flightData.flightNumber}
        model={flightData.model}
        registration={flightData.registration}
        groundSpeed={flightData.groundSpeed}
        loading={loading}
        totalAircraft={flightData.totalAircraft}
        lastUpdated={flightData.lastUpdated}
      />
    </main>
  )
} 