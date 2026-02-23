document.getElementById('wish-btn').addEventListener('click', function() {
    const name = document.getElementById('name').value.trim();
    const wishDisplay = document.getElementById('wish-display');
    
    if (name === '') {
        wishDisplay.innerHTML = '<p style="color: red;">Please enter a name!</p>';
        return;
    }
    
    const messages = [
        `Happy Birthday, ${name}! 🎂🎉 May your day be filled with joy and laughter! 🎈`,
        `Wishing you a fantastic birthday, ${name}! 🎉🥳 Hope all your dreams come true! 🌟`,
        `Cheers to another year of awesomeness, ${name}! 🥳🎊 Have a blast! 🎆`,
        `Happy Birthday, ${name}! 🎈🎂 You're amazing and deserve the best! 💖`,
        `May your birthday be as sweet as cake, ${name}! 🍰🎂 Enjoy every moment! 🎉`,
        `Another year wiser, ${name}! 🎊📅 Celebrate big and make memories! 📸`,
        `Happy Birthday, ${name}! 🌟⭐ You're a star and deserve all the happiness! 💫`,
        `Wishing you endless joy, ${name}! 🎈🎉 May your birthday be unforgettable! 🥂`,
        `Happy Birthday, ${name}! 🎂🍾 Here's to another amazing year! 🎊`
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    wishDisplay.innerHTML = `<p>${randomMessage}</p>`;
    wishDisplay.style.display = 'block';
});
