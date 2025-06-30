import FlightInfoDisplay from "@/components/flight-info-display"

export default function Home() {
  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-100">
      <FlightInfoDisplay flightNumber="ABC1234" model="A320" registration="N123AB" groundSpeed={452.75} />
    </main>
  )
} 