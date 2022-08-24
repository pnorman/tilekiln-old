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
	"encoding/json"
	"fmt"

	"github.com/pnorman/tilekiln/pkg/config"
)

const (
	Version   = "3.0.0"
	SchemeXYZ = "xyz"
	SchemeTMS = "tms"
)

var worldBounds = [4]float64{-180, -85.05112877980659, 180, 85.0511287798066}

/* See https://github.com/mapbox/tilejson-spec/tree/master/3.0.0 for definition
of TileJSON fields */

type VectorLayer struct {
	Id string `json:"id"`
}

type TileJSON struct {
	TileJSON     string        `json:"tilejson"`
	Tiles        []string      `json:"tiles"`
	VectorLayers []VectorLayer `json:"vector_layers"`
	Attribution  string        `json:"attribution,omitempty"`
	Bounds       [4]float64    `json:"bounds,omitempty"`
	Description  string        `json:"description,omitempty"`
	Maxzoom      uint8         `json:"maxzoom,omitempty"`
	Minzoom      uint8         `json:"minzoom,omitempty"`
	Name         string        `json:"name,omitempty"`
	Scheme       string        `json:"scheme,omitempty"`
	Version      string        `json:"version,omitempty"`
}

// GenerateTilejson takes a config and generates a Tilejson
func GenerateTileJSON(config config.Config, host string) ([]byte, error) {
	result := TileJSON{
		TileJSON:     Version,
		Tiles:        []string{fmt.Sprintf("%s{z}/{x}/{y}.mvt", host)},
		VectorLayers: make([]VectorLayer, 0),
		Attribution:  config.Metadata.Attribution,
		Bounds:       worldBounds,
		Description:  config.Metadata.Description,
		Name:         config.Metadata.Name,
		Scheme:       SchemeXYZ,
		Version:      config.Metadata.Version,
	}
	/* Still need to handle vector layers, min/max zoom */

	return json.MarshalIndent(result, "", "  ")
}
