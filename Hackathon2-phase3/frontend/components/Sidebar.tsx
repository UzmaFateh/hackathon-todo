'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, CheckSquare, Settings, MessageSquare, LogOut, User } from 'lucide-react';
import { signOut, useSession } from '@/lib/auth-client';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Sidebar({ className }: { className?: string }) {
    const pathname = usePathname();
    const { data: session } = useSession();

    const navItems = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Todos', href: '/dashboard/todos', icon: CheckSquare },
        { name: 'Chat', href: '/dashboard/chat', icon: MessageSquare },
        { name: 'Settings', href: '/dashboard/settings', icon: Settings },
    ];

    return (
        <div className={twMerge("flex flex-col h-full bg-white border-r border-gray-200", className)}>
            <div className="p-6 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                    T
                </div>
                <h1 className="text-xl font-bold text-gray-800 tracking-tight">My Tasks</h1>
            </div>

            <nav className="flex-1 px-4 space-y-2 py-4">
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={clsx(
                                "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
                                isActive
                                    ? "bg-primary-50 text-primary-700 font-medium shadow-sm"
                                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                            )}
                        >
                            <item.icon
                                className={clsx(
                                    "w-5 h-5 transition-colors",
                                    isActive ? "text-primary-500" : "text-gray-400 group-hover:text-gray-600"
                                )}
                            />
                            {item.name}
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-gray-200">
                <div className="flex items-center gap-3 mb-4 px-2">
                    <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500">
                        <User className="w-5 h-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                            {session?.user?.name || 'User'}
                        </p>
                        <p className="text-xs text-gray-500 truncate">
                            {session?.user?.email}
                        </p>
                    </div>
                </div>
                <button
                    onClick={async () => {
                        await signOut();
                        window.location.href = '/login';
                    }}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 bg-gray-50 hover:bg-red-50 hover:text-red-600 rounded-lg transition-all border border-gray-200 hover:border-red-200"
                >
                    <LogOut className="w-4 h-4" />
                    Sign Out
                </button>
            </div>
        </div>
    );
}
