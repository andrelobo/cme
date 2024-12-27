import React from 'react';
import { Link } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-white">
      <nav className="bg-wine-700 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold">CME System</Link>
          <div className="space-x-4">
            <Link to="/dashboard" className="hover:text-wine-200">Dashboard</Link>
            <Link to="/users" className="hover:text-wine-200">Users</Link>
            <Link to="/materials" className="hover:text-wine-200">Materials</Link>
          </div>
        </div>
      </nav>
      <main className="container mx-auto mt-8 px-4">
        {children}
      </main>
    </div>
  );
}

export default Layout;

