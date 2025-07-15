import React from 'react'
import WorkflowRunStatus from './components/WorkflowRunStatus'

function App() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">AgentFlow: Run Status</h1>
      <WorkflowRunStatus runId={1} />
    </div>
  )
}

export default App
