//using System;
//using System.Collections.Generic;
//using System.ComponentModel;
//using System.Data;
//using System.Drawing;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;
//using System.Windows.Forms;

//namespace NgeeAnnCity.UI
//{
//    public partial class Form1 : Form
//    {
//        public Form1()
//        {
//            InitializeComponent();
//        }
//    }
//}

using System;
using System.Drawing;
using System.Windows.Forms;

namespace Ngee_Ann_City
{
    public partial class Form1 : Form
    {
        private const int GridSize = 8;  // For testing; later change to 20 for Arcade mode
        private Button[,] gridButtons = new Button[GridSize, GridSize];

        public Form1()
        {
            //InitializeComponent();
            LoadGrid();
        }

        private void LoadGrid()
        {
            int tileSize = 60;
            this.ClientSize = new Size(GridSize * tileSize, GridSize * tileSize);  // Resize form to fit grid

            for (int row = 0; row < GridSize; row++)
            {
                for (int col = 0; col < GridSize; col++)
                {
                    Button tile = new Button
                    {
                        Size = new Size(tileSize, tileSize),
                        Location = new Point(col * tileSize, row * tileSize),
                        FlatStyle = FlatStyle.Flat,
                        Margin = Padding.Empty,
                        Tag = new Point(row, col),
                        BackColor = (row + col) % 2 == 0 ? Color.Beige : Color.LightGray,
                    };

                    tile.Click += Tile_Click;
                    this.Controls.Add(tile);
                    gridButtons[row, col] = tile;
                }
            }
        }

        private void Tile_Click(object sender, EventArgs e)
        {
            Button clickedTile = sender as Button;
            Point location = (Point)clickedTile.Tag;

            // For now: just mark tile as Residential (R)
            clickedTile.Text = "R";
            clickedTile.BackColor = Color.LightGreen;

            // Later: Connect to GameManager.PlaceBuilding(...)
        }
    }
}
