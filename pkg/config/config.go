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

package config

import (
	"fmt"
	"io/ioutil"
	"log"

	"gopkg.in/yaml.v3"
)

type Metadata struct {
	Id          string     `yaml:"id"`
	Bounds      [4]float64 `yaml:"bounds"`
	Name        string     `yaml:"name"`
	Description string     `yaml:"description"`
	Version     string     `yaml:"version"`
	Attribution string     `yaml:"attribution"`
	Center      [3]float64 `yaml:"center"`
}

type SqlDefinition struct {
	Minzoom uint8
	Maxzoom uint8
	Extent  uint32
	File    string
}

type VectorLayer struct {
	Description string            `yaml:"description"`
	Fields      map[string]string `yaml:"fields"`
	Sql         []SqlDefinition   `yaml:"sql"`
}

type Config struct {
	Metadata     Metadata               `yaml:"metadata"`
	VectorLayers map[string]VectorLayer `yaml:"vector_layers"`
}

func LoadConfig(file string) Config {
	f, err := ioutil.ReadFile(file)
	if err != nil {
		log.Fatal(err)
	}

	var config Config

	err = yaml.Unmarshal(f, &config)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Read config file " + file)
	return config
}
