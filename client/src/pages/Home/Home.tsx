import React from 'react';

const Home = () => {
  return (
    // Add min-h-screen to make sure it takes at least the full height of the viewport
    <section className="home section min-h-screen">
      {/* Use flex, flex-col, items-center, and justify-center to center the content */}
      <div className="flex flex-col items-center justify-center h-full mt-24">
        <h1 className="text-4xl font-bold mb-2">BusBuddy</h1>
        <p className="mb-8">
          Safe Rides, Happy Landings.
        </p>
        <img src="/BusBuddy.png" alt="BusBuddy Logo" className="w-64 rounded-full mb-8"/>
        <h1 className="mb-4 text-lg font-semibold"> Welcome to BusBuddies, the digital safety protection for your children on public transportation. </h1>
      </div>
    </section>
  );
};

export default Home;
