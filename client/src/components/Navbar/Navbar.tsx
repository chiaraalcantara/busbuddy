import { useContext } from 'react';
import UserContext from '../Contexts/UserContext';
import './Navbar.css';

const links = [
    { title: 'Home', href: '/' },
    { title: 'Map', href: '/map' },
    { title: 'Bus Register', href: '/bus-register'},
    { title: 'Login', href: '/login' },
];

// some use context for the register and the child profile
const Navbar = () => {

    const { user } = useContext(UserContext);


    return (
        // the green and w/o is just temp chnage later 
        <header className="w-full fixed top-0 left-0 z-auto bg-green-300 shadow-xl">
            <nav className='flex justify- container items-center gap-x-4 px-4 h-[50px]'>
                <h1 className="font-bold text-lg">Magic School Bus xD</h1>
                <ul className="flex gap-x-8">
                    {links.map((link, index) => (
                        <li key={index}>
                            {user && (
                                <a href={link.href} className="font-semibold">{link.title}</a>
                            )}
                        </li>
                    ))}
                </ul>
            </nav>
        </header>
    );
};

export default Navbar;
