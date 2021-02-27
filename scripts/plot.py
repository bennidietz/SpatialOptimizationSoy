cmap3 = ListedColormap(["#b3cc33","#10773e", "#be94e8","#1b5ee4"])
legend_landuse3 = [
        mpatches.Patch(color="#b3cc33",label = 'Soy'),
        mpatches.Patch(color="#10773e",label = 'Not soy'),
        mpatches.Patch(color="#be94e8",label = 'Urban areas and infrastructure'),
        mpatches.Patch(color="#1b5ee4",label = 'Water')
]

im1 = plt.imshow(landuse_original, interpolation='none',
        cmap=cmap2, vmin = 0.5, vmax = 5.5)
        ax2.set_title('Landuse map reclassified')
        ax2.set_xlabel('Column #')
        ax2.set_ylabel('Row #')
        ax2.legend(handles=legend_landuse3, bbox_to_anchor=(1.05,1), loc=2,
            borderaxespad=0.)
        plt.imsave(settings.get_file_landuse_reclass(), landuse_reclass, format = "tiff", cmap = cmap2)