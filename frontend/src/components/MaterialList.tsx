import React, { useState, useEffect } from "react";
import { getAllMaterials } from "../services/api";

interface Material {
  id: number;
  name: string;
  type: string;
  expiration_date: string;
  serial: string;
}

const MaterialList: React.FC = () => {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchMaterials = async () => {
      try {
        const data = await getAllMaterials();
        setMaterials(data);
      } catch (err) {
        setError("Failed to fetch materials. Please try again later.");
      }
    };
    fetchMaterials();
  }, []);

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-wine-700 mb-6">Material List</h2>
      <table className="min-w-full bg-white">
        <thead className="bg-wine-700 text-white">
          <tr>
            <th className="py-2 px-4 text-left">Name</th>
            <th className="py-2 px-4 text-left">Type</th>
            <th className="py-2 px-4 text-left">Expiration Date</th>
            <th className="py-2 px-4 text-left">Serial</th>
          </tr>
        </thead>
        <tbody>
          {materials.map((material) => (
            <tr key={material.id} className="border-b">
              <td className="py-2 px-4">{material.name}</td>
              <td className="py-2 px-4">{material.type}</td>
              <td className="py-2 px-4">{material.expiration_date}</td>
              <td className="py-2 px-4">{material.serial}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MaterialList;
