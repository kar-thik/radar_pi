import type React from "react"
import { ArrowRight, Plane } from "lucide-react"

interface FlightInfoDisplayProps {
  flightNumber: string
  model: string
  registration: string
  groundSpeed: number
}

export default function FlightInfoDisplay({ flightNumber, model, registration, groundSpeed }: FlightInfoDisplayProps) {
  return (
    <div className="w-[800px] h-[480px] bg-white text-gray-900 p-6 rounded-lg shadow-lg overflow-hidden relative border">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <Plane className="w-8 h-8 text-blue-600" />
          <h1 className="text-2xl font-bold tracking-tight">Flight Information</h1>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Last Updated</p>
          <p className="text-lg font-mono">{new Date().toLocaleTimeString()}</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-6">
          <InfoCard
            label="Flight Number"
            value={flightNumber}
            icon={
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="font-mono font-bold text-blue-600">#</span>
              </div>
            }
          />

          <InfoCard
            label="Aircraft Model"
            value={model}
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
            icon={
              <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <span className="font-mono font-bold text-green-600">R</span>
              </div>
            }
          />

          <InfoCard
            label="Ground Speed"
            value={`${groundSpeed.toFixed(2)} knots`}
            icon={
              <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                <ArrowRight className="w-5 h-5 text-red-600" />
              </div>
            }
          />
        </div>
      </div>

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 h-16 bg-gray-50 border-t flex items-center justify-end px-6">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-sm">System Active</span>
        </div>
      </div>
    </div>
  )
}

interface InfoCardProps {
  label: string
  value: string
  icon: React.ReactNode
}

function InfoCard({ label, value, icon }: InfoCardProps) {
  return (
    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
      <div className="flex items-center gap-3 mb-2">
        {icon}
        <span className="text-gray-600 text-sm uppercase tracking-wider">{label}</span>
      </div>
      <div className="pl-12">
        <span className="text-2xl font-mono font-semibold">{value}</span>
      </div>
    </div>
  )
} 