const svg = document.getElementById('svg');
const pieces = [];
for (let x = 0; x < 15; x++) {
  pieces.push([]);
  for (let y = 0; y < 15; y++) {
    const piece = document.createElementNS('http://www.w3.org/2000/svg', 'use');
    pieces[x].push(piece);
    piece.setAttribute('x', (x * 10 - 70).toString());
    piece.setAttribute('y', (y * 10 - 70).toString());
    piece.setAttribute('fill-opacity', '0');
    piece.setAttributeNS(
        'http://www.w3.org/1999/xlink', 'xlink:href', '#piece');
    piece.addEventListener('mouseenter', () => {
      if (piece.getAttribute('fill-opacity') === '1') return;
      piece.setAttribute('fill', game.black ? 'url(#black)' : 'url(#white)');
      piece.setAttribute('fill-opacity', '0.5');
    });
    piece.addEventListener('mouseleave', () => {
      if (piece.getAttribute('fill-opacity') === '1') return;
      piece.setAttribute('fill-opacity', '0');
    });
    piece.addEventListener('click', () => {
      if (game.winner || piece.getAttribute('fill-opacity') === '1') return;
      piece.setAttribute('fill', game.black ? 'url(#black)' : 'url(#white)');
      piece.setAttribute('fill-opacity', '1');
      dropPiece(x, y);
      if (!game.winner) {
        game.black = !game.black;
      }
    });
    svg.appendChild(piece);
  }
}

const mark = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
mark.setAttribute('fill', 'red');
mark.setAttribute('width', '2');
mark.setAttribute('height', '2');
mark.setAttribute('opacity', '0');
svg.appendChild(mark);

const dropPiece = (x, y) => {
  mark.setAttribute('x', (x * 10 - 71).toString());
  mark.setAttribute('y', (y * 10 - 71).toString());
  mark.setAttribute('opacity', '0.7');
  game.winner = checkWinner(x, y);
  if (game.winner) {
    Message(`游戏结束，${game.winner === 'black' ? '黑' : '白'}棋胜利！`);
  }
};

const checkWinner = (x, y) => {
  const color = pieces[x][y].getAttribute('fill');
  const potentialWinner = color === 'url(#black)' ? 'black' : 'white';
  const list = [4, 3, 2, 1];
  if (x >= 4) {
    if (!list.some(
            i => pieces[x - i][y].getAttribute('fill-opacity') !== '1' ||
                pieces[x - i][y].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
    if (y >= 4 &&
        !list.some(
            i => pieces[x - i][y - i].getAttribute('fill-opacity') !== '1' ||
                pieces[x - i][y - i].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
    if (y <= 10 &&
        !list.some(
            i => pieces[x - i][y + i].getAttribute('fill-opacity') !== '1' ||
                pieces[x - i][y + i].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
  }
  if (x <= 10) {
    if (!list.some(
            i => pieces[x + i][y].getAttribute('fill-opacity') !== '1' ||
                pieces[x + i][y].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
    if (y >= 4 &&
        !list.some(
            i => pieces[x + i][y - i].getAttribute('fill-opacity') !== '1' ||
                pieces[x + i][y - i].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
    if (y <= 10 &&
        !list.some(
            i => pieces[x + i][y + i].getAttribute('fill-opacity') !== '1' ||
                pieces[x + i][y + i].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
  }
  if (y >= 4) {
    if (!list.some(
            i => pieces[x][y - i].getAttribute('fill-opacity') !== '1' ||
                pieces[x][y - i].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
  }
  if (y <= 10) {
    if (!list.some(
            i => pieces[x][y + i].getAttribute('fill-opacity') !== '1' ||
                pieces[x][y + i].getAttribute('fill') !== color)) {
      return potentialWinner;
    }
  }
  return null;
};

const messageDiv = document.getElementById('message');
const Message = (content) => {
  const div = document.createElement('div');
  div.innerHTML = `<div>${content}</div>`;
  messageDiv.appendChild(div);
  setTimeout(() => messageDiv.removeChild(div), 3000);
};

const game = {
  black: true
};
