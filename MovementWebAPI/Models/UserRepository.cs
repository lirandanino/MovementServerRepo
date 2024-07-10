using MovementWebAPI.Data;

namespace MovementWebAPI.Models
{
    public class UserRepository : IUserRepository
    {

        private readonly MovementDbContext _context;


        public UserRepository(MovementDbContext context)
        {
            _context = context;
        }

        public IEnumerable<User> GetAllUsers()
        {
            return _context.Users.ToList();
        }

        public User GetUserById(int id)
        {
            return _context.Users.FirstOrDefault(u => u.ID == id);
        }

        public void CreateUser(User user)
        {
            _context.Users.Add(user);
            _context.SaveChanges();
        }

        public void UpdateUser(User user)
        {
            var existingUser = _context.Users.Find(user.ID);
            if (existingUser != null)
            {
                existingUser.LastName = user.LastName;
                existingUser.FirstName = user.FirstName;
                existingUser.Email = user.Email;
                existingUser.Avatar = user.Avatar;

                _context.SaveChanges();
            }
        }

        public void DeleteUser(int userId)
        {
            var user = _context.Users.Find(userId);
            if (user != null)
            {
                _context.Users.Remove(user);
                _context.SaveChanges();
            }

        }

  
    }
}
