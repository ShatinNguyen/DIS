document.addEventListener('DOMContentLoaded', function() {
    const board = document.getElementById('chessboard');
    const nextButton = document.createElement('button');
    nextButton.textContent = "Next Move";
    document.body.appendChild(nextButton);

    let currentMoveIndex = 0;
    let moves = []; // This will store the array of moves

    function displayMove(move) {
        // Logic to update the board based on `move`
        console.log("Displaying move", move);
    }

    nextButton.onclick = function() {
        if (currentMoveIndex < moves.length) {
            displayMove(moves[currentMoveIndex]);
            currentMoveIndex++;
        }
    };

    function fetchGame(gameId) {
        fetch(`/api/game/${gameId}`)
            .then(response => response.json())
            .then(gameData => {
                moves = gameData.moves; // Assuming the moves are in an array
                displayMove(moves[0]); // Start with the first move
            })
            .catch(error => console.error('Error fetching game:', error));
    }

    // Example: Fetch a game when the page loads
    fetchGame('some-game-id');
});
