using Microsoft.EntityFrameworkCore;
using MovementWebAPI.Models;

namespace MovementWebAPI.Data
{
    public class MovementDbContext : DbContext
    {

        public MovementDbContext(DbContextOptions<MovementDbContext> options)
              : base(options)
        {
        }

        public DbSet<User> Users { get; set; }


  
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure Student entity
            modelBuilder.Entity<User>(entity =>
            {
                entity.ToTable("Users"); // Set table name
                entity.HasKey(e => e.ID); // Set primary key
             

            });

        }
    }
}
