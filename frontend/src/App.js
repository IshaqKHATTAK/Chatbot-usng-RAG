import logo from './logo.svg';
import './App.css';
import InputBox from './components/InputBox';
import ChatWindow from './components/ChatWindow';


function App() {
  const instructions = (
    <p style={{ textAlign: 'center', marginTop: '1rem', marginBottom: '1rem' }}>
      Welcome! I am fodie bot an AI assistatn here to help you any query about the restourant.
    </p>
  );
  return (
    <div className="App" style={{border: '2px solid rgb(46, 134, 193)',backgroundColor: 'rgb(214, 234, 248)',width: '57%',margin: '0 auto'}}>
      {instructions}
     <ChatWindow/>
     
    </div>
  );
}

export default App;
