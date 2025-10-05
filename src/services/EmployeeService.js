import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const api = axios.create({
  baseURL: `${API_BASE_URL}/employees`,
});

export async function fetchEmployees() {
  try {
    const response = await api.get('');  // Changed from '/' to ''
    return response.data;
  } catch (error) {
    console.error('Error fetching employees:', error);
    throw error; 
  }
}

export async function createEmployee(employeeData) {
  try {
    const response = await api.post('', employeeData);  // Changed from '/' to ''
    return response.data;
  } catch (error) {
    console.error('Error creating employee:', error);
    throw error;
  }
}

export async function updateEmployee(id, employeeData) {
  try {
    const response = await api.put(`/${id}`, employeeData);
    return response.data;
  } catch (error) {
    console.error(`Error updating employee ${id}:`, error);
    throw error;
  }
}

export async function deleteEmployee(id) {
  try {
    const response = await api.delete(`/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting employee ${id}:`, error);
    throw error;
  }
}