const TaskFilters = ({ filters, setFilters }) => {
    const handleChange = (e) => {
      setFilters({ ...filters, [e.target.name]: e.target.value });
    };
  
    return (
      <div>
        <label>Filter by Priority: </label>
        <select name="priority" value={filters.priority} onChange={handleChange}>
          <option value="">All</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
  
        <label>Sort by Due Date: </label>
        <select name="sortByDueDate" value={filters.sortByDueDate} onChange={handleChange}>
          <option value="">Default</option>
          <option value="asc">Oldest First</option>
          <option value="desc">Newest First</option>
        </select>
      </div>
    );
  };
  
  export default TaskFilters;
  