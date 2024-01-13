// import React from 'react';
import './Navbar.css';

const links = [
    { title: 'Home', href: '/' },
    { title: 'Map', href: '/map' },
    { title: 'Login', href: '/login' },
];

// some use context for the register and the child profile
const Navbar = () => {
    return (
        // the green and w/o is just temp chnage later
        <header className="w-full fixed top-0 left-0 z-1000 bg-green-300 shadow-xl">
            <nav className='flex justify-between container items-center gap-x-4 px-4 h-[50px]'>
                <h1 className="font-bold text-lg">Magic School Bus xD</h1>
                <ul className="flex gap-x-8">
                    {links.map((link, index) => (
                        <li key={index}>
                            <a href={link.href} className="font-semibold">{link.title}</a>
                        </li>
                    ))}
                </ul>
            </nav>
        </header>
    );
};

export default Navbar;
