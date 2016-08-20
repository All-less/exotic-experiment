/**
 * Logo generator for exotic experiment.
 *
 * @see  https://github.com/shrhdk/text-to-svg
 */

const options = {
    fontSize: 24,
    anchor: "left top",
    attributes: {
        className: "path"
    }
}
const text = 'E X O T I C'
const textToSVG = require('text-to-svg').loadSync("fonts/Helvetica.ttf");
const svg = textToSVG.getPath(text, options);
console.log(svg);
console.log(textToSVG.getMetrics(text, options));
