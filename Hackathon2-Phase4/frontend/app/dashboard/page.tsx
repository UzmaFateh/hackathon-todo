'use client';

import { useEffect, useState } from 'react';
import { getTasks, Task } from '@/lib/api';
import useApi from '@/lib/useApi';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { CheckCircle2, Circle, Clock, AlertTriangle } from 'lucide-react';

export default function DashboardPage() {
    const tasksApi = useApi<Task[]>();
    const [tasks, setTasks] = useState<Task[]>([]);

    useEffect(() => {
        tasksApi.execute(() => getTasks());
    }, []);

    useEffect(() => {
        if (tasksApi.data) {
            setTasks(tasksApi.data);
        }
    }, [tasksApi.data]);

    // Calculate stats
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(t => t.is_completed).length;
    const pendingTasks = totalTasks - completedTasks;
    const highPriorityTasks = tasks.filter(t => t.priority === 'high' && !t.is_completed).length;

    // Chart Data
    const statusData = [
        { name: 'Completed', value: completedTasks },
        { name: 'Pending', value: pendingTasks },
    ];

    const priorityData = [
        { name: 'High', value: tasks.filter(t => t.priority === 'high').length },
        { name: 'Medium', value: tasks.filter(t => t.priority === 'medium').length },
        { name: 'Low', value: tasks.filter(t => t.priority === 'low').length },
    ];

    const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6'];

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
                <p className="text-gray-500">Welcome back! Here's what's happening with your tasks.</p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-gray-500 font-medium">Total Tasks</h3>
                        <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                            <Circle className="w-5 h-5" />
                        </div>
                    </div>
                    <p className="text-3xl font-bold text-gray-900">{totalTasks}</p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-gray-500 font-medium">Completed</h3>
                        <div className="p-2 bg-green-50 text-green-600 rounded-lg">
                            <CheckCircle2 className="w-5 h-5" />
                        </div>
                    </div>
                    <p className="text-3xl font-bold text-gray-900">{completedTasks}</p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-gray-500 font-medium">Pending</h3>
                        <div className="p-2 bg-amber-50 text-amber-600 rounded-lg">
                            <Clock className="w-5 h-5" />
                        </div>
                    </div>
                    <p className="text-3xl font-bold text-gray-900">{pendingTasks}</p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-gray-500 font-medium">High Priority</h3>
                        <div className="p-2 bg-red-50 text-red-600 rounded-lg">
                            <AlertTriangle className="w-5 h-5" />
                        </div>
                    </div>
                    <p className="text-3xl font-bold text-gray-900">{highPriorityTasks}</p>
                </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Status Chart */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <h3 className="text-lg font-semibold text-gray-900 mb-6">Task Status</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={statusData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {statusData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Priority Chart */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <h3 className="text-lg font-semibold text-gray-900 mb-6">Tasks by Priority</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={priorityData}>
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
}
