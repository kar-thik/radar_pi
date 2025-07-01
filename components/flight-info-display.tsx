import type React from "react"
import { ArrowRight, Plane, Clock, Users } from "lucide-react"
import { FlightInfoDisplayProps } from "@/types/flight"

export default function FlightInfoDisplay({ 
  flightNumber, 
  model, 
  registration, 
  groundSpeed, 
  loading = false,
  totalAircraft,
  lastUpdated
}: FlightInfoDisplayProps) {
  const currentTime = new Date().toLocaleTimeString()
  
  return (
    <div className="w-[800px] h-[480px] bg-white text-gray-900 p-6 rounded-lg shadow-lg overflow-hidden relative border">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <Plane className={`w-8 h-8 text-blue-600 ${loading ? 'animate-pulse' : ''}`} />
          <h1 className="text-2xl font-bold tracking-tight">Flight Information</h1>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Current Time</p>
          <p className="text-lg font-mono">{currentTime}</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-6">
          <InfoCard
            label="Flight Number"
            value={flightNumber}
            loading={loading}
            icon={
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="font-mono font-bold text-blue-600">#</span>
              </div>
            }
          />

          <InfoCard
            label="Aircraft Model"
            value={model}
            loading={loading}
            icon={
              <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                <span className="font-mono font-bold text-purple-600">M</span>
              </div>
            }
          />
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          <InfoCard
            label="Registration"
            value={registration}
            loading={loading}
            icon={
              <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <span className="font-mono font-bold text-green-600">R</span>
              </div>
            }
          />

          <InfoCard
            label="Ground Speed"
            value={`${groundSpeed.toFixed(2)} knots`}
            loading={loading}
            icon={
              <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                <ArrowRight className="w-5 h-5 text-red-600" />
              </div>
            }
          />
        </div>
      </div>

      {/* Additional Info Bar */}
      {(totalAircraft !== undefined || lastUpdated) && (
        <div className="absolute bottom-16 left-6 right-6 h-12 bg-blue-50 border border-blue-200 rounded-lg flex items-center justify-between px-4">
          {totalAircraft !== undefined && (
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-blue-600" />
              <span className="text-sm text-blue-700">
                {totalAircraft} aircraft nearby
              </span>
            </div>
          )}
          {lastUpdated && (
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-blue-600" />
              <span className="text-sm text-blue-700">
                Data: {new Date(lastUpdated).toLocaleTimeString()}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 h-16 bg-gray-50 border-t flex items-center justify-end px-6">
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${loading ? 'bg-yellow-500 animate-pulse' : 'bg-green-500 animate-pulse'}`}></div>
          <span className="text-sm">{loading ? 'Loading...' : 'System Active'}</span>
        </div>
      </div>
    </div>
  )
}

interface InfoCardProps {
  label: string
  value: string
  icon: React.ReactNode
  loading?: boolean
}

function InfoCard({ label, value, icon, loading = false }: InfoCardProps) {
  return (
    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
      <div className="flex items-center gap-3 mb-2">
        {icon}
        <span className="text-gray-600 text-sm uppercase tracking-wider">{label}</span>
      </div>
      <div className="pl-12">
        <span className={`text-2xl font-mono font-semibold ${loading ? 'animate-pulse bg-gray-300 text-gray-300 rounded' : ''}`}>
          {value}
        </span>
      </div>
    </div>
  )
} 