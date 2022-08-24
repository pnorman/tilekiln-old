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
package cmd

import (
	"fmt"
	"log"

	"github.com/pnorman/tilekiln/pkg/config"
	"github.com/pnorman/tilekiln/pkg/tilejson"
	"github.com/spf13/cobra"
)

// tilejsonCmd represents the tilejson command
var tilejsonCmd = &cobra.Command{
	Use:   "tilejson",
	Short: "Produce a tilejson from a configuration",
	Long:  `Produce a tilejson from a configuration`,
	Run: func(cmd *cobra.Command, args []string) {
		result, err := tilejson.GenerateTileJSON(config.LoadConfig(configFile), "http://127.0.0.1:8080/")
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(string(result))
	},
}

func init() {
	rootCmd.AddCommand(tilejsonCmd)
}
