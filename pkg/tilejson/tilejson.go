/*
Copyright © 2022 Paul Norman <osm@paulnorman.ca>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

package tilejson

import (
	"github.com/pnorman/tilekiln/pkg/config"
)

const Version = "3.0.0"

type VectorLayer struct {
	Id string `json:"id"`
}

type TileJSON struct {
	TileJSON     string      `json:"tilejson"`
	Tiles        []string    `json:"tiles"`
	VectorLayers VectorLayer `json:"vector_layers"`
	Attribution  string      `json:"attribution"`
	Bounds       [4]float64  `yaml:"bounds"`
	Description  string      `json:"description"`
	Maxzoom      uint8       `json:"maxzoom"`
	Minzoom      uint8       `json:"minzoom"`
	Name         string      `json:"name"`
	Scheme       string      `json:"scheme"`
	Version      string      `json:"version"`
}

// GenerateTilejson takes a config and generates a Tilejson
func GenerateTileJSON(config config.Config) string {
	return "{}"
}
