import { requestMoveFromML } from './src/requestMoveFromML.mjs';

// App Component/Containter/Whatever
// Everyone loves putting their webpage inside an App component these days.
class App extends HTMLElement {
  constructor() {
    super();
    // Turn whatever text was inside the tags into the starting log. Eg. <app>prompt text</app>
    this.gameLog = this.innerText.replace(/\n+/g, '\n');
    this.currentPlayer = 'X';
    this.state = [0,0,0,0,0,0,0,0,0];
    this.lastMove = ['None', 'None'];
    this.innerHTML = `
    <h2>Next Move: <span class="player-label">${this.currentPlayer}</span></h2>
    <div class="gameboard">
      <div class="banner">Waiting...</div>
      ${this.state.map((cell, idx) => 
                       `<div class="cell" data-idx="${idx}"></div>`).join('')}
    </div>
    <pre class="game-log">${this.gameLog}</pre>
    `;
    
    // Start the Log with the empty board.
    this.gameLog += this.toString();
    this.renderGameLog();
    this.renderStateReady();
  }
  
  /* Add/Remove event listeners */
  connectedCallback() {
    this.addEventListener('click', this.handleClick);
    this.addEventListener('submit-move', this.handleSubmitMove)
  }
  disconnectedCallback() {
    this.removeEventListener('click', this.handleClick);
    this.removeEventListener('submit-move', this.handleSubmitMove);
  }
  

  
  /* (re)renders the current player mark. */
  renderActivePlayer() {
    const elm = this.querySelector('.player-label');
    elm.innerText = this.currentPlayer;
  }
  /* (re)renders the gameboard grid. */
  renderGamestate() {
    document.querySelectorAll('.cell').forEach(elm => {
      const idx = parseInt(elm.dataset.idx, 10);
      const mark = this.state[idx] ? this.state[idx] : ''
      elm.innerText = mark;
    }); 
  }
  /* (re)render the game log. */
  renderGameLog() {
    const elm = this.querySelector('.game-log');
    elm.innerText = this.gameLog;
    // Keep it scrolled to the bottom.
    elm.scroll(0, elm.scrollHeight);
  }
  /* Render Waiting/Active State */
  renderStateWaiting() {
    const elm = this.querySelector('.banner');
    elm.innerText = 'Waiting...';
    elm.style.display = 'block';
  }
  renderStateReady() {
    const elm = this.querySelector('.banner');
    elm.style.display = 'none';
  }
  renderStateError() {
    const elm = this.querySelector('.banner');
    elm.innerText = 'Error';
    elm.style.display = 'block';
  }
  /* (re)render everything */
  render() {
    this.renderGamestate()
    this.renderActivePlayer();
    this.renderGameLog();
  }
  
  
  /* Click to play a move */
  async handleClick(evt) {
    const { target } = evt;
    // bail if the click was not on a cell.
    if (!target.classList.contains('cell')) { return; }
    // get the cell index.
    const idx = parseFloat(target.dataset.idx);
    // Play the move
    this.play(this.currentPlayer, idx);

    // For Demo, simulate a response
    this.renderStateWaiting();
    // this.respondAsAsync(idx);
    // this.requestMLMove();
    const mlResponse = await requestMoveFromML(this.gameLog);
    console.log('mlResponse', mlResponse);
  }
  
  /* API to play a move */
  handleSubmitMove(evt) {
    const { value = '' } = evt.detail;
    const lines = value.split('\n');
    const lineLastPlay = lines.filter(line => line.startsWith("Last Play:"));
    if (lineLastPlay.length !== 1) {
      return this.logError(`Invalid Response. No "Last Play:"`, value);
    }
    const lastPlay = lineLastPlay[0].split(':')[1].split(',');
    const lastMark = lastPlay[0].trim();
    if (lastMark !== this.currentPlayer) {
      return this.logError(`Invalid Response.\nExpected "Last Play: ${this.currentPlayer}, ${lastPlay[1]}" `, lineLastPlay);
    }
    let lastIdx
    try {
      lastIdx = parseInt(lastPlay[1], 10);
      if (isNaN(lastIdx) || lastIdx < 0 || lastIdx > 8) {
        throw new Error(`Expected "${lastIdx}" to be a value be a number between 0-8`);
      }
      // Play the move
      this.play(lastMark, lastIdx);
      // Unlock the state.
      this.renderStateReady();
    }
    catch (err) {
      console.log('err', err);
      return this.logError(`Invalid Response.\n${err}`, lineLastPlay);
    }
  }
 
  
  // Returns the string version of the value at state[idx]
  at(idx) {
    const value = this.state[idx]
    if (value === 0) { return ' '; }
    return value;
  }
  
  /* Plays Mark at Idx */
  play(mark, idx) {
    // Update State
    this.lastMove = [mark, idx];
    this.state[idx] = mark;
    this.currentPlayer = mark === 'X' ? 'O' : 'X';
    // Update the log.
    this.gameLog += this.toString();
    // Re-render state.
    this.render()
  } 
  
  
  /* Convert the Gamestate into a text string.  */
  toString() {
    return `\n
Next Play: ${this.currentPlayer}
Last Play: ${this.lastMove[0]}, ${this.lastMove[1]}
 ${this.at(0)} | ${this.at(1)} | ${this.at(2)}  
 ${this.at(3)} | ${this.at(4)} | ${this.at(5)}  
 ${this.at(6)} | ${this.at(7)} | ${this.at(8)}  
`;
  }
  
  logError(msg, raw) {
    this.gameLog += `
===[[ Error in Response ]]===
${msg}
---[[ Raw Response ]]---
${raw}
===[[ End ]]===
    `;
    this.renderGameLog();
    this.renderStateError();
  }
  
  // Pretend to be an async endpoint responding.
  // respondAsAsync(userMove) {
  //   setTimeout(() => {
  //     const response = RESPONSES[userMove];
  //     const moveEvent = new CustomEvent('submit-move', {
  //       detail: {
  //         value: response,
  //       }
  //     });
  //     this.dispatchEvent(moveEvent);
  //   }, 1000 * (1 + Math.random()));
  // }

}
customElements.define("app-ttt-game", App);





const RESPONSES = {
4: `
Next Play: X
Last Play: O, 6
   |   |    
   | X |    
 O |   |   
`,
0: `
Next Play: X
Last Play: O, 8
 X |   |    
   | X |    
 O |   | O  
`,
7: `
Next Play: X
Last Play: O, 1
 X | O |    
   | X |    
 O | X | O  
`,
8: `
Next Play: X
Last Play: X, 1
 X | O |    
   | X |    
 O | X | O  
`,
6: `
Next Play: X
Last Play: O, 10
   |   |    
   | X |    
   |   |   
`,
1: `
Next Play: X
Last Play: O, forfit
   | X |    
   |   |    
   |   |   
`,  
}