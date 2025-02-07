import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#2b2a28] text-[#f4e6d4] text-center px-6">
      <h1 className="text-5xl font-bold mb-6 text-[#e3b578]">Welcome to Task Manager</h1>
      <p className="text-lg text-[#d6c1a8] max-w-xl">
        Organize your tasks effortlessly with our intuitive Task Manager. Plan, prioritize, and track your progress in a beautifully designed workspace.
      </p>

      <div className="mt-8 space-x-6">
        <Link 
          to="/login" 
          className="bg-[#8c5b3e] text-[#f4e6d4] px-6 py-3 rounded-lg hover:bg-[#73462e] transition shadow-lg"
        >
          Login
        </Link>
        <Link 
          to="/register" 
          className="bg-[#627c58] text-[#f4e6d4] px-6 py-3 rounded-lg hover:bg-[#4e6445] transition shadow-lg"
        >
          Register
        </Link>
      </div>
    </div>
  );
};

export default Home;
