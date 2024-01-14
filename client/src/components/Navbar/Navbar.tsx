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

       // Function to determine if a link should be shown based on user state
       const shouldShowLink = (title) => {
        if (user) return true; // logged in users can see all
        return title === 'Home' || title === 'Login'; // not logged in users see Home and Login
    };

    return (
        // the green and w/o is just temp chnage later
        //bg-green-300 shadow-xl
        <header className="w-full fixed top-0 left-0 z-1000">
            <nav className='flex justify-between container items-center gap-x-4 px-4 h-[70px]'>
                <h1 className="font-bold text-lg">Magic School Bus xD</h1>
                <ul className="flex gap-x-8">
                    {links.filter(link => shouldShowLink(link.title)).map((link, index) => (
                        <li key={index}>
                            <a href={link.href} className="hover:underline font-semibold">{link.title}</a>
                        </li>
                    ))}
                </ul>
            </nav>
        </header>
    );
};

export default Navbar;
