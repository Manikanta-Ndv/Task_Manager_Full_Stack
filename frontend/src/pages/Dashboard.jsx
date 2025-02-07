import { useEffect, useState, useContext } from "react";
import { getTasks } from "../api";
import { AuthContext } from "../context/AuthContext";
import TaskForm from "../components/TaskForm";
import TaskItem from "../components/TaskItem";
import TaskFilters from "../components/TaskFilter";

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [tasks, setTasks] = useState([]);
  const [filters, setFilters] = useState({ priority: "", sortByDueDate: "" });
  const [page, setPage] = useState(1);
  const [pageSize] = useState(5);
  const [totalPages, setTotalPages] = useState(1);

  const fetchTasks = () => {
    getTasks(null, filters, page, pageSize).then((res) => {
      console.log("Fetched Data:", res.data); // ✅ Debugging
      setTasks(res.data.tasks || []);
      setTotalPages(res.data.totalPages || 1);
    }).catch(error => {
      console.error("Error fetching tasks:", error);
    });
  };

  useEffect(() => {
    fetchTasks();
  }, [user, filters, page]);

  if (!user)
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-50 text-gray-700">
        <p className="text-lg font-semibold">Please log in to view your tasks.</p>
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-100 p-6 pt-20 flex justify-center">
      <div className="w-full max-w-4xl bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-3xl font-bold text-center text-gray-800">Task Dashboard</h2>

        {/* Task Filters */}
        <div className="my-4">
          <TaskFilters filters={filters} setFilters={setFilters} />
        </div>

        {/* Task Form */}
        <div className="mb-6">
          <TaskForm refreshTasks={fetchTasks} token={user.token} />
        </div>

        {/* Task List */}
        {tasks.length === 0 ? (
        <p className="text-center text-gray-500 text-lg mt-4">No tasks found.</p>
         ) : (
          <ul className="mt-4 space-y-4">
            {tasks?.map((task) => (
            <li key={task.id} className="bg-gray-50 p-4 rounded-lg shadow-sm hover:shadow-md transition-all">
            <TaskItem task={task} refreshTasks={fetchTasks} token={user.token} />
            </li>
            ))}
          </ul>
        )}

        {/* Pagination Controls */}
        <div className="flex justify-between items-center mt-6">
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
            className={`px-4 py-2 rounded-lg transition-all ${
              page === 1
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-blue-600 text-white hover:bg-blue-700"
            }`}
          >
            ← Previous
          </button>
          <span className="text-gray-700 font-medium">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(page + 1)}
            disabled={page === totalPages}
            className={`px-4 py-2 rounded-lg transition-all ${
              page === totalPages
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-blue-600 text-white hover:bg-blue-700"
            }`}
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
