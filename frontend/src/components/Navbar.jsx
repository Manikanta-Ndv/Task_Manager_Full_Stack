import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="fixed top-0 left-0 w-full bg-white/80 backdrop-blur-md shadow-md py-4 px-6 flex justify-between items-center z-50">
      {/* Logo */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="text-2xl font-bold text-gray-900"
      >
        <Link to="/">Task<span className="text-blue-600">Manager</span></Link>
      </motion.div>

      {/* Navigation Links */}
      <div className="flex items-center space-x-6">
        <NavItem to="/" label="Home" />
        {user && <NavItem to="/dashboard" label="Dashboard" />}
        {user && <NavItem to="/profile" label="Profile" />}

        {/* Auth Buttons */}
        {user ? (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={logout}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-all shadow-md"
          >
            Logout
          </motion.button>
        ) : (
          <>
            <NavItem to="/login" label="Login" />
            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
              <Link
                to="/register"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-all shadow-md"
              >
                Register
              </Link>
            </motion.div>
          </>
        )}
      </div>
    </nav>
  );
};

// Reusable Nav Item Component
const NavItem = ({ to, label }) => (
  <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
    <Link to={to} className="text-gray-700 hover:text-blue-600 font-medium transition">
      {label}
    </Link>
  </motion.div>
);

export default Navbar;
