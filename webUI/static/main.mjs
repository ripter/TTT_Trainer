import { requestMoveFromML } from './src/requestMoveFromML.mjs';
import { getWinner } from './src/getWinner.mjs';

const GAME_MODE = {
  READY: 'READY',
  WAITING: 'WAITING',
  ERROR: 'ERROR',
  X_WON: 'X_WON',
  O_WON: 'O_WON',
  TIE: 'TIE',
};

// App Component/Containter/Whatever
// Everyone loves putting their webpage inside an App component these days.
class App extends HTMLElement {
  #_gameMode; // one of GAME_MODE
  set gameMode(val) {
    if (Object.values(GAME_MODE).indexOf(val) === -1) {
      throw new Error(`Invalid gameMode: \nRecived "${val}"\nExpected ${Object.values(GAME_MODE).join(' | ')}`);
    }
    this.#_gameMode = val;
    this.renderGameMode(); 
  }
  get gameMode() {
    return this.#_gameMode;
  }

  constructor() {
    super();
    // Turn whatever text was inside the tags into the starting log. Eg. <app>prompt text</app>
    this.gameLog = this.innerText.replace(/\n+/g, '\n');
    // Replace children with the game board.
    this.state = [0,0,0,0,0,0,0,0,0];
    this.currentPlayer = 'X';
    this._initInnerHTML();
    // this.#_gameMode = 'READY';
    this.lastMove = ['None', 'None'];
    
    // Start the Log with the empty board.
    this.gameMode = GAME_MODE.READY;
    this.gameLog += this.toString();
    this.renderGameLog();
  }
  
  /* Add/Remove event listeners */
  connectedCallback() {
    this.addEventListener('click', this.handleClick);
    // this.addEventListener('submit-move', this.handleSubmitMove)
  }
  disconnectedCallback() {
    this.removeEventListener('click', this.handleClick);
    // this.removeEventListener('submit-move', this.handleSubmitMove);
  }
  
  _initInnerHTML() {
    this.innerHTML = `
    <h2>Next Move: <span class="player-label">${this.currentPlayer}</span></h2>
    <div class="gameboard">
      <div class="banner">Waiting...</div>
      ${this.state.map((cell, idx) =>
      `<div class="cell" data-idx="${idx}"></div>`).join('')}
    </div>
    <pre class="game-log">${this.gameLog}</pre>
    `;
  }

  
  renderGameMode() {
    const banner = this.querySelector('.banner');
    switch (this.#_gameMode) {
      case 'READY':
        banner.style.display = 'none';
        break;
      case 'WAITING':
        banner.innerText = 'Waiting...';
        banner.style.display = 'block';
        break;
      case 'ERROR':
        banner.innerText = 'Llama Spit!';
        banner.style.display = 'block';
        break;
      case 'X_WON':
        banner.innerText = 'X Wins!';
        banner.style.display = 'block';
        break;
      case 'O_WON':
        banner.innerText = 'O Wins!';
        banner.style.display = 'block';
        break;
      case 'TIE':
        banner.innerText = 'Tie Game!';
        banner.style.display = 'block';
        break;
    }
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
  /* (re)render everything */
  render() {
    this.renderGamestate()
    this.renderActivePlayer();
    this.renderGameLog();
  }


  async handleClick(evt) {
    // Only handle clicks when the game is ready.
    if (this.gameMode !== GAME_MODE.READY) { return; }

    const { target } = evt;
    // bail if the click was not on a cell.
    if (!target.classList.contains('cell')) { return; }

    // get the cell index.
    const idx = parseFloat(target.dataset.idx);
    this.humanClickToPlay(idx); 
  }
  
  
  /*  
   * Event Handlers
   * The User Clicks a Cell to Play.
  */
  async humanClickToPlay(idx) {
    // Play the move
    this.play(this.currentPlayer, idx);
    // Did the player win?
    const winner = getWinner(this.state);
    if (winner) {
      this.gameLog += `Winner: ${winner}`;
      if (winner === 'X') {
        this.gameMode = GAME_MODE.X_WON;
      } else if (winner === 'O') {
        this.gameMode = GAME_MODE.O_WON;
      } else if (winner === 'T') {
        this.gameMode = GAME_MODE.TIE;
      }
      return;
    }

    // Time for the AI to play.
    // Show waiting while we wait for the response.
    this.gameMode = GAME_MODE.WAITING;
    // Request the AI to play a move. 
    const mlResponse = await requestMoveFromML(this.gameLog);
    // Process the AI's response.
    this.aiClickToPlay(mlResponse);
    this.gameMode = GAME_MODE.READY;
  }

  async aiClickToPlay(responseText) {
    const lines = responseText.split('\n');
    const lineLastPlay = lines.filter(line => line.toLowerCase().startsWith("last play:"));
    if (lineLastPlay.length !== 1) {
      if (lineLastPlay.length > 1) {
        return this.logError(`Invalid Response.\nResponse containted more than one move.`, value);
      }
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
      return this.play(lastMark, lastIdx);
    }
    catch (err) {
      console.log('err', err);
      return this.logError(`Invalid Response.\n${err}`, lineLastPlay);
    }
  }
  
  /* API to play a move */
  // handleSubmitMove(evt) {
  //   const { value = '' } = evt.detail;
  //   const lines = value.split('\n');
  //   const lineLastPlay = lines.filter(line => line.toLowerCase().startsWith("last play:"));
  //   if (lineLastPlay.length !== 1) {
  //     if (lineLastPlay.length > 1) {
  //       return this.logError(`Invalid Response.\nResponse containted more than one move.`, value);
  //     }
  //     return this.logError(`Invalid Response. No "Last Play:"`, value);
  //   }
  //   const lastPlay = lineLastPlay[0].split(':')[1].split(',');
  //   const lastMark = lastPlay[0].trim();
  //   if (lastMark !== this.currentPlayer) {
  //     return this.logError(`Invalid Response.\nExpected "Last Play: ${this.currentPlayer}, ${lastPlay[1]}" `, lineLastPlay);
  //   }
  //   let lastIdx
  //   try {
  //     lastIdx = parseInt(lastPlay[1], 10);
  //     if (isNaN(lastIdx) || lastIdx < 0 || lastIdx > 8) {
  //       throw new Error(`Expected "${lastIdx}" to be a value be a number between 0-8`);
  //     }
  //     // Play the move
  //     this.play(lastMark, lastIdx);
  //     // Unlock the state.
  //     this.renderStateReady();
  //   }
  //   catch (err) {
  //     console.log('err', err);
  //     return this.logError(`Invalid Response.\n${err}`, lineLastPlay);
  //   }
  // }
 
  
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
    this._waiting = true; // Lock the state.
    this.gameLog += `
===[[ Error in Response ]]===
${msg}
---[[ Raw Response ]]---
${raw}
===[[ End ]]===
    `;
    this.renderGameLog();
  }
}
customElements.define("app-ttt-game", App);