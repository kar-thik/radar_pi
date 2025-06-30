import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    const filePath = path.join(process.cwd(), 'flight_data.json')
    
    // Check if file exists
    if (!fs.existsSync(filePath)) {
      return NextResponse.json({
        error: 'Flight data not available',
        flightNumber: 'NO DATA',
        model: 'Unknown',
        registration: 'Unknown',
        groundSpeed: 0,
        altitude: 'Unknown',
        lastUpdated: new Date().toISOString(),
        totalAircraft: 0
      })
    }
    
    const fileContent = fs.readFileSync(filePath, 'utf8')
    const flightData = JSON.parse(fileContent)
    
    return NextResponse.json(flightData)
  } catch (error) {
    console.error('Error reading flight data:', error)
    return NextResponse.json({
      error: 'Failed to load flight data',
      flightNumber: 'ERROR',
      model: 'Unknown',
      registration: 'Unknown',
      groundSpeed: 0,
      altitude: 'Unknown',
      lastUpdated: new Date().toISOString(),
      totalAircraft: 0
    })
  }
} 