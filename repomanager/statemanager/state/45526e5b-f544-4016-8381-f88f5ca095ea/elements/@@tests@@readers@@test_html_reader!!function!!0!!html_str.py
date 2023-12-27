def html_str() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Sections Example</title>
</head>
<body>
    <header>
        <h1>Welcome to My Website</h1>
    </header>

    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
        </ul>
    </nav>

    <section id="about">
        <h2>About Us</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
    </section>

    <section id="services">
        <h2>Our Services</h2>
        <ul>
            <li>Service 1</li>
            <li>Service 2</li>
            <li>Service 3</li>
        </ul>
    </section>

    <section>
        <h2>Contact Us</h2>
        <p>You can reach us at \
<a href="mailto:contact@example.com">contact@example.com</a>.</p>
    </section>

    <footer>
        <p>&copy; 2023 My Website</p>
    </footer>
</body>
</html>
"""