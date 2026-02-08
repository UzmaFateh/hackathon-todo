'use client';

import { useState, useEffect } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { Menu, X, Loader2 } from 'lucide-react';
import { clsx } from 'clsx';
import { getSession } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const session = await getSession();
                if (!session) {
                    router.push('/login');
                } else {
                    setLoading(false);
                }
            } catch (error) {
                console.error("Auth check failed", error);
                router.push('/login');
            }
        };
        checkAuth();
    }, [router]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <Loader2 className="h-8 w-8 animate-spin text-primary-500" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 w-full">
            {/* Mobile Header */}
            <div className="lg:hidden flex items-center justify-between p-4 bg-white border-b border-gray-200 sticky top-0 z-20">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white font-bold shadow-sm">
                        T
                    </div>
                    <span className="font-bold text-gray-800">My Tasks</span>
                </div>
                <button
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    className="p-2 rounded-lg hover:bg-gray-100 text-gray-600"
                >
                    {isSidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                </button>
            </div>

            <div className="flex h-screen overflow-hidden">
                {/* Sidebar for Desktop */}
                <div className="hidden lg:block w-64 flex-shrink-0 h-full">
                    <Sidebar />
                </div>

                {/* Sidebar for Mobile (Drawer) */}
                <div
                    className={clsx(
                        "fixed inset-0 z-30 lg:hidden transition-opacity duration-300",
                        isSidebarOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
                    )}
                >
                    <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setIsSidebarOpen(false)} />
                    <div
                        className={clsx(
                            "absolute top-0 left-0 bottom-0 w-64 bg-white shadow-xl transform transition-transform duration-300",
                            isSidebarOpen ? "translate-x-0" : "-translate-x-full"
                        )}
                    >
                        <Sidebar />
                    </div>
                </div>

                {/* Main Content */}
                <main className="flex-1 overflow-auto p-4 sm:p-6 lg:p-8 w-full">
                    <div className="max-w-7xl mx-auto">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
