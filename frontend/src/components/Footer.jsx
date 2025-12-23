import { PROJECT, STUDENTS } from '../constants';
import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <p className="footer-label">Developed by</p>
          <div className="footer-students">
            {STUDENTS.map((student) => (
              <div key={student.id} className="student-card">
                <span className="student-name">{student.name}</span>
                <span className="student-id">ID: {student.id}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;