import { useEffect, useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000' // change if different

function WorkflowRunStatus({ runId }) {
  const [run, setRun] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchRunStatus = async () => {
      try {
        const res = await axios.get(`${API_BASE}/runs/${runId}`)
        setRun(res.data)
        setLoading(false)

        if (res.data.status === 'running' || res.data.status === 'pending') {
          setTimeout(fetchRunStatus, 2000) // poll every 2s
        }
      } catch (err) {
        console.error('Error fetching run:', err)
      }
    }

    fetchRunStatus()
  }, [runId])

  if (loading) return <p>Loading run info...</p>

  return (
    <div className="border p-4 rounded bg-gray-50">
      <p><strong>Status:</strong> {run.status}</p>
      <p><strong>Started At:</strong> {new Date(run.started_at).toLocaleString()}</p>
      {run.ended_at && (
        <p><strong>Ended At:</strong> {new Date(run.ended_at).toLocaleString()}</p>
      )}

      <h3 className="mt-4 font-semibold">Logs:</h3>
      <pre className="bg-white p-3 rounded mt-2 text-sm overflow-x-auto">
        {JSON.stringify(run.logs, null, 2)}
      </pre>
    </div>
  )
}

export default WorkflowRunStatus
