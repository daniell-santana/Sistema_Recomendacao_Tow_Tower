import { useState } from 'react';
import { CoursePage } from './components/CoursePage';
import { UserProfile } from './components/UserProfile';

export interface CourseInterest {
  id: string;
  courseName: string;
  selectedUnit: string;
  selectedDay: string;
  selectedShift: string;
  registeredDate: Date;
}

function App() {
  const [currentView, setCurrentView] = useState<'course' | 'profile'>('course');
  const [courseInterests, setCourseInterests] = useState<CourseInterest[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleRegisterInterest = (interest: Omit<CourseInterest, 'id' | 'registeredDate'>) => {
    const newInterest: CourseInterest = {
      ...interest,
      id: Math.random().toString(36).substr(2, 9),
      registeredDate: new Date(),
    };
    setCourseInterests([...courseInterests, newInterest]);
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <div className="min-h-screen bg-[#121212]">
      {currentView === 'course' ? (
        <CoursePage
          onRegisterInterest={handleRegisterInterest}
          onNavigateToProfile={() => setCurrentView('profile')}
          isLoggedIn={isLoggedIn}
          onLogin={handleLogin}
        />
      ) : (
        <UserProfile
          courseInterests={courseInterests}
          onNavigateToCourse={() => setCurrentView('course')}
        />
      )}
    </div>
  );
}

export default App;