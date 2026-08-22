import OperationCard from "./OperationCard";

function OperationList({ missions, searchQuery, onSearchChange, onUpdateMission, onDeleteMission }) {
  return (
    <div className="ops-panel">
      <h2 className="panel-title">Active Field Manifest</h2>
      
      <input
        type="text"
        className="ops-input"
        placeholder="FILTER STRATEGIC DATA..."
        value={searchQuery}
        onChange={(e) => onSearchChange(e.target.value)}
      />
      
      <div className="feed-grid">
        {missions && missions.length > 0 ? (
          missions.map((mission) => (
            <OperationCard 
              key={mission.id}
              mission={mission}
              onUpdateMission={onUpdateMission}
              onDeleteMission={onDeleteMission}
            />
          ))
        ) : (
          <p className="text-gray-500 tracking-wider uppercase text-sm p-4">
            No classified records match the query.
          </p>
        )}
      </div>
    </div>
  );
}

export default OperationList;
