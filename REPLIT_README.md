# Michael Ditter Website with Bitcoin and AI Reports

This project contains Michael Ditter's personal website with enhanced Bitcoin and AI reports using Shadcn UI components and real-time data.

## Features

- **Real-time Bitcoin Report**: Displays current Bitcoin price, market data, and insights that update automatically.
- **AI Market Research Chart**: Visualizes ChatGPT dominance in India compared to other AI chatbots, with interactive Chart.js charts.
- **Shadcn UI Components**: Modern, responsive UI components for a clean user experience.

## Running the Project in Replit

1. Click the "Run" button to start the server
2. View the website in the preview pane
3. The Bitcoin data will update automatically every 5 minutes

## Project Structure

- **index.html**: Main website with Bitcoin and AI report sections
- **js/main.js**: Contains JavaScript for fetching Bitcoin data and rendering Charts
- **css/custom-overrides.css**: Styling for the Bitcoin and AI report components
- **bitcoin-research-api/**: API for fetching Bitcoin data

## Development

To modify the project:

1. Edit the HTML in `index.html` to change the layout and content
2. Modify `js/main.js` to change the Bitcoin data fetching or Chart.js configurations
3. Update styles in `css/custom-overrides.css` to change the appearance
4. Run the dev server with `npm run dev`

## API Endpoints

- **/bitcoin-research-api/api/bitcoin-data**: Returns current Bitcoin price and market data

## Creating New Reports

To create a new Bitcoin or AI report:

1. Duplicate the existing report sections in `index.html`
2. Update the data sources and chart configurations in `js/main.js`
3. Add any new CSS styles to `css/custom-overrides.css`

## Additional Resources

- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [Shadcn UI Documentation](https://ui.shadcn.com/) 