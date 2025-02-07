import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="bg-white shadow-md py-4 px-6 flex justify-between items-center fixed w-full top-0 z-50">
      <div className="text-2xl font-bold text-gray-800">
        <Link to="/">TaskManager</Link>
      </div>
      
      <div className="space-x-6">
        <Link to="/" className="text-gray-600 hover:text-blue-600 font-medium transition">Home</Link>
        {user && <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 font-medium transition">Dashboard</Link>}
        {user && <Link to="/profile" className="text-gray-600 hover:text-blue-600 font-medium transition">Profile</Link>}

        {user ? (
          <button 
            onClick={logout} 
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition shadow-md"
          >
            Logout
          </button>
        ) : (
          <>
            <Link to="/login" className="text-gray-600 hover:text-blue-600 font-medium transition">Login</Link>
            <Link to="/register" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition shadow-md">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
