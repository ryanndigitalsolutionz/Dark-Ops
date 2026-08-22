import { useState } from "react";
import OperationForm from "./components/OperationForm";
import OperationList from "./components/OperationList";
import "./App.css";

function App() {
  const [missions, setMissions] = useState([
    {
      "id": "1",
      "title": "Operation EMP Shutdown",
      "description": "Deploy electromagnetic counter-measures to mask localized signature profiles across orbit sectors."
    },
    {
      "id": "2",
      "title": "Project Vibrant Metal",
      "description": "Secure heavy drilling heavy machinery logs from extraction zones before corporate scanning systems trigger."
    },
    {
      "id": "3",
      "title": "Operation Sovereign Grid",
      "description": "Establish a tactical closed power system footprint to decouple critical comms infrastructure from external networks."
    },
    {
      "id": "4",
      "title": "Project Aegis Infiltration",
      "description": "Bypass simulation layers to verify orbital shield telemetry alignments without tripping security warnings."
    },
    {
      "id": "5",
      "title": "Operation Platinum Vault",
      "description": "Synchronize distributed transaction ledgers to back physical stone warehouse assets against inflationary trends."
    },
    {
      "id": "6",
      "title": "Project Alpha Mimic",
      "description": "Run localized behavioral matrix variations within virtual test servers to monitor systemic adaptation metrics."
    }
  ]);
  
  const [searchQuery, setSearchQuery] = useState("");

  function handleAddMission(newMission) {
    const missionWithId = { ...newMission, id: Date.now().toString() };
    setMissions((prev) => [...prev, missionWithId]);
  }

  function handleUpdateMission(updatedMission) {
    setMissions((prev) =>
      prev.map((m) => (m.id === updatedMission.id ? updatedMission : m))
    );
  }

  function handleDeleteMission(id) {
    setMissions((prev) => prev.filter((m) => m.id !== id));
  }

  const filteredMissions = missions.filter((mission) =>
    mission.title ? mission.title.toLowerCase().includes(searchQuery.toLowerCase()) : false
  );

  return (
    <div className="ops-wrapper">
      <header>
        <h1 className="ops-title">Agency Command Platform</h1>
      </header>
      
      <main>
        {/* Fixed component tag here */}
        <OperationForm onAddMission={handleAddMission} /> 
        <OperationList 
          missions={filteredMissions} 
          searchQuery={searchQuery} 
          onSearchChange={setSearchQuery}
          onUpdateMission={handleUpdateMission}
          onDeleteMission={handleDeleteMission}
        />
      </main>
    </div>
  );
}

export default App;
