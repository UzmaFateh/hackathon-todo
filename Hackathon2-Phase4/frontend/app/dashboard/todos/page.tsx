'use client';

import { useState, useEffect } from 'react';
import { getTasks, Task, apiRequest } from '@/lib/api';
import useApi from '@/lib/useApi';
import TaskItem from '@/components/TaskItem';
import ErrorBoundary from '@/components/ErrorBoundary';
import { PrioritySelector } from '@/components/PrioritySelector';
import { TagInput } from '@/components/TagInput';
import { SearchBar } from '@/components/SearchBar';
import { FilterPanel } from '@/components/FilterPanel';
import { SortControls } from '@/components/SortControls';
import TaskSkeleton from '@/components/TaskSkeleton';
import { Plus } from 'lucide-react';

export default function TodosPage() {
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [newTaskPriority, setNewTaskPriority] = useState<"high" | "medium" | "low">("medium");
    const [newTaskTags, setNewTaskTags] = useState<string[]>([]);
    const [availableTags, setAvailableTags] = useState<string[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [statusFilter, setStatusFilter] = useState('all');
    const [priorityFilter, setPriorityFilter] = useState('all');
    const [datePresetFilter, setDatePresetFilter] = useState('all');
    const [sortBy, setSortBy] = useState('created_at');
    const [sortOrder, setSortOrder] = useState('desc');

    const tasksApi = useApi<Task[]>();
    const createApi = useApi<Task>();

    // Load tasks and tags
    useEffect(() => {
        const loadData = async () => {
            await tasksApi.execute(() => getTasks(searchQuery, statusFilter, priorityFilter, datePresetFilter, sortBy, sortOrder));
            try {
                const tags = await apiRequest<Array<{ name: string }>>('/api/tags');
                setAvailableTags(tags.map(t => t.name));
            } catch (error) {
                console.error('Failed to load tags:', error);
            }
        };

        loadData();
    }, [searchQuery, statusFilter, priorityFilter, datePresetFilter, sortBy, sortOrder]);

    const [tasks, setTasks] = useState<Task[]>(tasksApi.data || []);

    useEffect(() => {
        if (tasksApi.data) {
            setTasks(tasksApi.data);
        }
    }, [tasksApi.data]);

    const handleCreateTask = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!newTaskTitle.trim()) return;

        const newTask = await createApi.execute(() =>
            apiRequest<Task>('/api/tasks', {
                method: 'POST',
                body: JSON.stringify({
                    title: newTaskTitle.trim(),
                    priority: newTaskPriority,
                    tags: newTaskTags
                }),
            })
        );

        if (newTask && !createApi.error) {
            setTasks(prevTasks => [...prevTasks, newTask]);
            setNewTaskTitle('');
            setNewTaskPriority("medium");
            setNewTaskTags([]);

            // Refresh tags
            try {
                const tags = await apiRequest<Array<{ name: string }>>('/api/tags');
                setAvailableTags(tags.map(t => t.name));
            } catch (error) {
                console.error('Failed to refresh tags:', error);
            }
        }
    };

    const handleTaskUpdated = (updatedTask: Task) => {
        setTasks(prevTasks => prevTasks.map(task =>
            task.id === updatedTask.id ? updatedTask : task
        ));
    };

    const handleTaskDeleted = (taskId: number) => {
        setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
    };

    return (
        <ErrorBoundary>
            <div className="space-y-6">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
                    <p className="text-gray-500">Manage and organize your daily tasks.</p>
                </div>

                {tasksApi.error && (
                    <div className="p-4 bg-red-50 border border-red-100 text-red-700 rounded-xl shadow-sm">
                        Failed to load tasks: {tasksApi.error.message}. Please refresh the page.
                    </div>
                )}

                {createApi.error && (
                    <div className="p-4 bg-red-50 border border-red-100 text-red-700 rounded-xl shadow-sm">
                        Failed to create task: {createApi.error.message}. Please try again.
                    </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Sidebar / Controls */}
                    <div className="lg:col-span-4 space-y-6">
                        {/* Add Task Panel */}
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                                <Plus className="h-5 w-5 text-primary-500" />
                                New Task
                            </h2>
                            <form onSubmit={handleCreateTask} className="space-y-4">
                                <input
                                    type="text"
                                    value={newTaskTitle}
                                    onChange={(e) => setNewTaskTitle(e.target.value)}
                                    placeholder="What needs to be done?"
                                    className="input-luxury"
                                    disabled={createApi.loading}
                                />

                                <div className="space-y-3">
                                    <label className="text-xs font-medium text-gray-500 uppercase tracking-wider ml-1">Priority</label>
                                    <PrioritySelector
                                        value={newTaskPriority}
                                        onChange={setNewTaskPriority}
                                        disabled={createApi.loading}
                                    />
                                </div>

                                <div className="space-y-3">
                                    <label className="text-xs font-medium text-gray-500 uppercase tracking-wider ml-1">Tags</label>
                                    <TagInput
                                        value={newTaskTags}
                                        onChange={setNewTaskTags}
                                        availableTags={availableTags}
                                        disabled={createApi.loading}
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className={`btn-luxury w-full mt-2 flex justify-center items-center ${createApi.loading ? 'opacity-70' : ''}`}
                                    disabled={createApi.loading}
                                >
                                    {createApi.loading ? 'Adding...' : 'Add Task'}
                                </button>
                            </form>
                        </div>

                        {/* Filters Panel */}
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <h2 className="text-lg font-semibold text-gray-800 mb-4">Filters</h2>
                            <FilterPanel
                                status={statusFilter}
                                priority={priorityFilter}
                                datePreset={datePresetFilter}
                                onStatusChange={setStatusFilter}
                                onPriorityChange={setPriorityFilter}
                                onDatePresetChange={setDatePresetFilter}
                            />
                        </div>
                    </div>

                    {/* Main Content / List */}
                    <div className="lg:col-span-8 space-y-6">
                        {/* Search & Sort */}
                        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col sm:flex-row gap-4 items-center justify-between">
                            <div className="w-full sm:w-2/3">
                                <SearchBar
                                    value={searchQuery}
                                    onChange={setSearchQuery}
                                    placeholder="Search tasks..."
                                />
                            </div>
                            <div className="w-full sm:w-auto">
                                <SortControls
                                    sortBy={sortBy}
                                    sortOrder={sortOrder}
                                    onSortByChange={setSortBy}
                                    onSortOrderChange={setSortOrder}
                                />
                            </div>
                        </div>

                        {/* Tasks List */}
                        <div className="space-y-4">
                            {tasksApi.loading ? (
                                Array.from({ length: 3 }).map((_, index) => (
                                    <TaskSkeleton key={`skeleton-${index}`} />
                                ))
                            ) : tasks.length === 0 ? (
                                <div className="bg-white p-12 rounded-xl shadow-sm border border-gray-100 text-center">
                                    <div className="w-20 h-20 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-4">
                                        <Plus className="h-10 w-10 text-primary-300" />
                                    </div>
                                    <h3 className="text-xl font-medium text-gray-800 mb-2">No tasks found</h3>
                                    <p className="text-gray-500">
                                        {searchQuery || statusFilter !== 'all'
                                            ? "Try adjusting your filters or search query"
                                            : "Create a new task to get started"}
                                    </p>
                                </div>
                            ) : (
                                tasks.map((task) => (
                                    <TaskItem
                                        key={task.id}
                                        task={task}
                                        onTaskUpdated={handleTaskUpdated}
                                        onTaskDeleted={handleTaskDeleted}
                                    />
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </ErrorBoundary>
    );
}
