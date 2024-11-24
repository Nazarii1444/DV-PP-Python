package main

import (
	"encoding/csv"
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"image/png"
	"math"
	"os"
	"strconv"
	"time"
)

type OHLCV struct {
	Time   time.Time
	Close  float64
	High   float64
	Low    float64
	Open   float64
	Volume float64
}

func writeResultsToFile(filename string, averageVolume, highestPrice float64) error {
	// записує результати у файл
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.WriteString(fmt.Sprintf("Average Volume: %.2f\n", averageVolume))
	if err != nil {
		return err
	}

	_, err = file.WriteString(fmt.Sprintf("Highest Closing Price: %.2f\n", highestPrice))
	if err != nil {
		return err
	}

	return nil
}

func loadCSV(filename string) ([]OHLCV, error) {
	// loadCSV завантажує OHLCV з CSV файлу
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	var data []OHLCV
	for i, record := range records {
		if i == 0 {
			continue // пропускаємо перший рядок
		}

		parsedTime, err := time.Parse("2006-01-02 15:04:05-07:00", record[0])
		if err != nil {
			return nil, fmt.Errorf("error parsing time at row %d: %v", i+1, err)
		}

		closePrice, _ := strconv.ParseFloat(record[2], 64)
		highPrice, _ := strconv.ParseFloat(record[3], 64)
		lowPrice, _ := strconv.ParseFloat(record[4], 64)
		openPrice, _ := strconv.ParseFloat(record[5], 64)
		volumePrice, _ := strconv.ParseFloat(record[6], 64)

		data = append(data, OHLCV{
			Time:   parsedTime,
			Close:  closePrice,
			High:   highPrice,
			Low:    lowPrice,
			Open:   openPrice,
			Volume: volumePrice,
		})
	}

	return data, nil
}

func calculateAverageVolume(data []OHLCV) float64 {
	// calculateAverageVolume знаходить середній об’єм торгів
	var totalVolume float64
	for _, entry := range data {
		totalVolume += entry.Volume
	}
	return totalVolume / float64(len(data))
}

func findHighestPrice(data []OHLCV) float64 {
	// findHighestPrice знаходить найвищу ціну серед даних
	highest := math.Inf(-1)
	for _, entry := range data {
		if entry.High > highest {
			highest = entry.High
		}
	}
	return highest
}

func generateChart(data []OHLCV, outputFilename string) error {
	// generateChart створює криву з Close значень та зберігає в PNG
	width := 1200
	height := 800
	margin := 50

	img := image.NewRGBA(image.Rect(0, 0, width, height))
	background := color.RGBA{R: 255, G: 255, B: 255, A: 255}
	draw.Draw(img, img.Bounds(), &image.Uniform{background}, image.Point{}, draw.Src)

	// Знаходимо min та max Close значення
	minClose, maxClose := data[0].Close, data[0].Close
	for _, entry := range data {
		if entry.Close < minClose {
			minClose = entry.Close
		}
		if entry.Close > maxClose {
			maxClose = entry.Close
		}
	}

	// Малює осі
	axesColor := color.RGBA{R: 0, G: 0, B: 0, A: 255}
	for x := margin; x < width-margin; x++ {
		img.Set(x, height-margin, axesColor)
	}
	for y := margin; y < height-margin; y++ {
		img.Set(margin, y, axesColor)
	}

	lineColor := color.RGBA{R: 0, G: 0, B: 255, A: 255}
	previousX, previousY := 0, 0
	for i, entry := range data {
		x := margin + i*(width-2*margin)/len(data)
		y := height - margin - int((entry.Close-minClose)/(maxClose-minClose)*float64(height-2*margin))

		if i > 0 {
			drawLine(img, previousX, previousY, x, y, lineColor)
		}

		previousX, previousY = x, y
	}

	file, err := os.Create(outputFilename)
	if err != nil {
		return err
	}
	defer file.Close()

	return png.Encode(file, img)
}

func drawLine(img *image.RGBA, x1, y1, x2, y2 int, col color.Color) {
	// Малює лінію на картинці між двома точками
	dx := abs(x2 - x1)
	dy := abs(y2 - y1)
	sx := -1
	if x1 < x2 {
		sx = 1
	}
	sy := -1
	if y1 < y2 {
		sy = 1
	}
	err := dx - dy

	for {
		img.Set(x1, y1, col)
		if x1 == x2 && y1 == y2 {
			break
		}
		e2 := 2 * err
		if e2 > -dy {
			err -= dy
			x1 += sx
		}
		if e2 < dx {
			err += dx
			y1 += sy
		}
	}
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	data, err := loadCSV("financial_data.csv")
	if err != nil {
		fmt.Printf("Error loading CSV: %v\n", err)
		return
	}

	err = generateChart(data, "chart.png")
	if err != nil {
		fmt.Printf("Error generating chart: %v\n", err)
		return
	}

	averageVolume := calculateAverageVolume(data)
	highestPrice := findHighestPrice(data)

	err = writeResultsToFile("analysis_results.txt", averageVolume, highestPrice)
	if err != nil {
		fmt.Printf("Error writing results to file: %v\n", err)
		return
	}

	fmt.Println("Збережено графік у файл 'chart.png'")
	fmt.Println("Збережено результати аналізу як 'analysis_results.txt'")
}
